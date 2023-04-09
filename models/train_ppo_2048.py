from wrapper import EnvironmentWrapper
from train_ppo_base import ActorCritic, PPO_Buffer, PPO_Trainer, train_ppo

def plot_2048_training(stats_file='ppo_2048_stats.json', w_size=20, dpi=300):
    """
    Generate a line plot of the average reward over the number of steps taken during training.
    """
    with open(stats_file, "r") as f:
        stats = json.load(f)

    window_size = w_size 
    rolling_avg_reward = np.convolve(stats["avg_reward"], np.ones(window_size)/window_size, mode='valid')
    rolling_num_steps = stats["num_steps"][window_size-1:]

    plt.plot(rolling_num_steps, rolling_avg_reward)
    plt.xlabel("NumSteps")
    plt.ylabel("Avg Reward")
    plt.title("PPO 2048 Training")
    plt.savefig("ppo_2048_training_smooth.png", dpi=dpi)
    plt.show()

if __name__ == "__main__":

    # Hyperparameters for model
    SHARED_HIDDEN_LAYER_SIZE= 512
    NUM_SHARED_LAYERS = 3
    ACTIVATION = nn.ReLU()
    PPO_CLIP_VAL = 0.20
    PPO_POLICY_LR = 3e-4
    PPO_VALUE_LR = 3e-3
    PPO_EPOCHS = 32
    VAL_EPOCHS = 32
    KL_TARGET = 0.02
    N_EPISODES = 250
    PRINT_FREQ = 1
    NUM_ROLLOUTS = 2
    SAVE_FREQ = 50 

    ###  TRAINS MODEL USING PROXIMAL POLICY OPTIMIZATION FOR 2048 ###

    # set up environment
    env = EnvironmentWrapper() 

    # set up model
    model = ActorCritic(env.observation_space_len, 
                        env.action_space.action_space_len, 
                        hidden_layer_size=SHARED_HIDDEN_LAYER_SIZE, 
                        num_shared_layers=NUM_SHARED_LAYERS, 
                        activation_function=ACTIVATION)
    model = model.to(DEVICE)  

    # set up PPO trainer
    ppo = PPO_Trainer(
        actor_critic = model, 
        ppo_clip_val = PPO_CLIP_VAL,
        ppo_lr = PPO_POLICY_LR,
        val_lr = PPO_VALUE_LR,
        ppo_epochs = PPO_EPOCHS, 
        val_epochs = VAL_EPOCHS,
        kl_earlystopping = KL_TARGET
    )

    # set up buffer
    ppobuffer = PPO_Buffer() 

    # train the model with PPO
    train_ppo(env=env, model=model, ppo_trainer=ppo, ppo_buffer = ppobuffer, model_path="ppo_2048_model", stats_path ="ppo_2048_stats.json")

    ###  PLOTS TRAINING AND EVALUATES TRAINED MODEL FOR PROXIMAL POLICY OPTIMIZATION ###

    # plot the training cartpole stats
    plot_2048_training('ppo_2048_stats.json')

