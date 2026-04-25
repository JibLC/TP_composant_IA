# How to build your AI component

The task is to build an AI component whose main objective is to predict the welding state from a given image.

As it was explained in the main presentation, the aim of this challenge is to build an AI component which take an image of welding as input and return as output , the predicted class of the welding (OK , KO) or UNKNOWN . UNKNOWN is used to say that model is not sure about the predicted class. As we will see later in the evaluation process an unknown output can be less penalizing than a False Negative (meaning a true KO predicted as OK) that have a critical cost.

From the evaluation process point of view , the AI component is considered as a black box. It means that the full evaluation process is only based on inference results of the submitted AI component on different datasets. It is not needed to access to the AI component architecture, layers, or gradient of neural network.

Thus, the submitted zip folder to codabench by participant shall be buildable as a python package :

A requirements.txt file listing all dependencies with exact versions of needed packages.

A setup.py file that will be used to build the python package of your AI component. This setup shall use the requirement.txt file.

A MANIFEST.IN file that is needed to list all additionnal files that are not python files you may have added to be used in your challenge_solution folder to ensure that they will be integrated in your AI component python package.

A folder named "challenge_solution" containing the source code of your AI component. This folder shall contain at least two files :

__init__.py : This is a file that is necessary to ensure that all files in this directory will be integrated to the python package of your component when it will be built .
AIComponent.py : The interface module of your AI component that shall contain a class named MyAIComponent describing the interface of your component. This class shall have at least two main methods that will be used by the evaluation pipeline named :
load_model() : load whatever is needed in the virtual env to be able to use the predict method .
predict() : Perform predictions on a list of input images, and return the list of predictions.
This interface class shall statisfy the following abstract class given here
[(opens new window)](https://github.com/confianceai/Challenge-Welding-Starter-Kit/blob/main/challenge_welding/ai_component_interface.py)

class AbstractAIComponent(ABC):
    """
    Abstract base class for AI components interface.
    """
    def __init__(self):
        self.AI_Component=None
        self.AI_component_meta_informations={}
    @abstractmethod
    def load_model(self,config_file=None):
        """
        Abstract method to load the model into the AI Component.
        Should be implemented by all subclasses.
        
        Parameters:
            config file : str
                A optional config file that could be used for the AI component loading
        
        """
        pass

    @abstractmethod
    def predict(self, input_images: list[np.ndarray], images_meta_informations: list[dict], device : str ) -> dict :
        """
        Abstract method to make predictions using the AI component.
        
        Parameters:
            input_images: list[np.ndarrays]
                The list of images numpy arrays
            images_meta_information: list[dict]
                The list of images metadata dictionaries 
                
        Returns:
            A dict containing 3 keys "predictions", "probabilities", "OOD_scores"(optional). 
                predictions : A list of the predictions given by the AI component among 3 possible values [KO, OK UNKNOWN"]
                probabilities : A list of 3-values lists containing predicted scores for each sample in this order [proba KO, proba OK, proba UNKNOWN]. sum of proba shall be 1 for each lists  
                OOD_scores : A list of  OOD score predicted by the AI component for each sample. An ood score is a real positive number. The image is considered OOD when this score is >=1

        """
        pass


To sum-up, your AI component shall have at least the following files and folder :

setup.py
MANIFEST.in
requirements.txt
challenge_solution/
    __init__.py
	AIComponent.py
You are free to add any other files you need to this structure in order to make your AI component working.

To access those additional files declared in MANIFEST.in (for example a file containing weights of your model) within in your AI_component.py code , you will need to add the following line, as done in the example(opens new window)

ROOT_PATH = Path(__file__).parent.resolve()

Then in your class MyAIComponent, you can access your file with path ROOT_PATH/yourfile.

## Inputs to the AI component
The AI component shall take the following inputs:

A list of numpy arrays representing the input images to process .
A list of dictionnaries containing a meta-description of the images
During the evaluation process, the following fields will be passed with the images:

welding-seams
resolution
Thus, the predict method of your AI component can suppose that the following fields are available and can be used in the prediction process :

image_meta_information["welding-seams"]
image_meta_information["resolution"]
An example of such input could be :

[{"welding-seams":"c102","resolution":["1920","1080"]},..,{"welding-seams":"c45","resolution":["960","540"]}]

## Outputs of the AI component

It shall return a dictionary with three keys `{predictions, probabilities (optional), OOD_score (optional)}`

The first key is required:

- *predictions* : The list of predicted welding state. The welding state can have three possible values: `[OK, KO, UNKNOWN]`

The following keys are not mandatory, but their presence will significantly contribute to the improvement of the quality score for the developed AI component:

- *probabilities* : The list of associated probabilities for each image. The list should have the format: $[P_{KO}, P_{OK}, P_{UNKNOWN}]$ where $\sum_{i \in \{OK, KO, UNKNOWN\}} P_i = 1$.

- *OOD_scores* : The list of OOD scores predicted by the AI component for each image. This score (X) is a real positive number. If $0 \leq X < 1$ the image is considered as *In-Domain*, if $X > 1$ the image is considered as *Out-of-Domain (OoD)*.

## Reference Solution
The github repository (opens new window)contains the code of a naive reference solution proposed for the Welding Quality Detection challenge. This solution is provided as a pedagogical example only and should not be considered a benchmark in terms of performance.

This repository contains four examples Jupyter notebooks that are described as follows:

01-Tutorial.ipynb: This script demonstrates how to use the main user functions present in this package. It includes examples of how to list available datasets, explore metadata, and draw basic statistics on contextual variables.

02-Create_pytorch_dataloader.ipynb: This script shows how to use the package to create a PyTorch dataloader.

03-Test_AIComponent.ipynb: This script demonstrates how to load an AI component and evaluate it by generating operational and uncertainty metrics.

04-Submit_Solution.ipynb : This notebook shows how to submit a solution to codabench

## Starting kit
This repository (opens new window)contains a template (opens new window)to create your own AI component. You can use it to:

Complete the myAIComponent class in this script (opens new window)by filling load_model() and predict() methods which are required so that the evaluation process can interact with your component.
Complete the setup.py (opens new window)with the needed information.
complete the requirements.txt (opens new window)with your own dependencies.
Complete the MANIFEST.in (opens new window)with any files you add in the challenge_solution folder (opens new window)so that your AI component works.
for any issues, write us an email at: challenge.confiance@irt-systemx.fr