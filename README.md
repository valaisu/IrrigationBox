# IrrigationBox
Programs needed to run an automated irrigation system, 
and evaluate it's success.

# Sub-projects:

# Sled and irrigation control:
  Key parts of the project are the sled and the water pump.
  The idea is to move a watering hose with the sled, which
  allows us to provide different parts of the box with 
  different amount of water. Pictures are taken to evaluate
  the plant growth in different areas. 
  # Move sled
    # Sled location calibration 
  # Pump water
  # Take pictures

# Evaluate plant size  
  To make the plant size evaluation scientific, there needs
  to be an algorithm for it. I want the algorithm to be run
  entirely by a computer

  Idea 1: Create a machine learning algorithm for detecting
  how much of the picture is covered by a plant. To train 
  the model, I would take pictures of plants, divide them 
  to sub-pictures, label the subpictures by how big area is
  covered by plant, and train the ML model with that data. 
  # Labeling
    # Create sub-pictures
    # Label the pictures
  
