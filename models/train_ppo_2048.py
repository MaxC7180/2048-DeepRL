# deep learning modules 
import torch
import torch.nn as nn 

# plotting / utility modules 
import numpy as np 
import matplotlib.pyplot as plt
import json

# internal modules 
from ppo_wrapper import EnvironmentWrapper
from train_ppo_base import * 

def plot_2048_training(stats_file='ppo_2048_stats.json', w_size=20, dpi=300):
    """
    Generates a line plot of the average reward over the number of steps taken during training.

    Args:
    - stats_file (str): the path to the JSON file containing the training statistics (default: 'ppo_2048_stats.json')
    - w_size (int): the size of the rolling window used for smoothing the plot (default: 20)
    - dpi (int): the resolution of the saved image file (default: 300)
    """
    # Load the training statistics from the specified file
    with open(stats_file, "r") as f:
        stats = json.load(f)

    # Smooth the data using a rolling average with the specified window size
    window_size = w_size 
    rolling_avg_reward = np.convolve(stats["avg_reward"], np.ones(window_size)/window_size, mode='valid')
    rolling_num_steps = stats["num_steps"][window_size-1:]

    # Generate the plot and save it to a file
    plt.plot(rolling_num_steps, rolling_avg_reward)
    plt.xlabel("NumSteps")
    plt.ylabel("Avg Reward")
    plt.title("PPO 2048 Training")
    plt.savefig("ppo_2048_training_smooth.png", dpi=dpi)
    plt.show()

if __name__ == "__main__":
    
    # set up device on which to update 
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    # Hyperparameters for model
    SHARED_HIDDEN_LAYER_SIZE= 256
    NUM_SHARED_LAYERS = 1
    ACTIVATION = nn.Tanh()
    PPO_CLIP_VAL = 0.20
    PPO_POLICY_LR = 1e-5
    PPO_VALUE_LR = 1e-4
    PPO_EPOCHS = 60
    VAL_EPOCHS = 60
    KL_TARGET = 0.02
    N_EPISODES = 20000
    PRINT_FREQ = 1
    NUM_ROLLOUTS = 16
    SAVE_FREQ = 50

    ###  TRAINS MODEL USING PROXIMAL POLICY OPTIMIZATION FOR 2048 ###

    # set up environment
    env = EnvironmentWrapper() 

    # set up model
    model = ActorCritic(
        obs_size=env.observation_space_len,
        act_size=env.action_space_len,
        hidden_layer_size=SHARED_HIDDEN_LAYER_SIZE,
        num_shared_layers=NUM_SHARED_LAYERS,
        activation_function=ACTIVATION,
    )

    model = model.to(DEVICE)  
    model.load_state_dict(torch.load('ppo_2048_model_rewardfinal14_11200.pt', map_location = DEVICE))

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
    train_ppo(env=env, model=model, ppo_trainer=ppo, ppo_buffer = ppobuffer,n_episodes=N_EPISODES, num_rollouts=NUM_ROLLOUTS, print_freq=PRINT_FREQ, save_freq=SAVE_FREQ, save_model=True, model_path="ppo_2048_model_rewardfinal15", stats_path ="ppo_2048_stats_rewardfinal15.json", load_from_checkpoint=True)
    


