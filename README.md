<!--
 * @Author: Yuhao_Wu
 * @Date: 2022-08-02 23:17:39
 * @LastEditors: Yuhao_Wu
 * @LastEditTime: 2022-08-04 14:40:37
 * @Description: 
-->
# A System of user-based Collaborative Filtering on MovieLens-small

## Dependancies
Please install python dependencies based on the versions in requirements.txt.
- (Optional): if you use **conda** to manage python virtual environments, to avoid make current conda enviroment messy, please create a new one and switch to it as below:
    > conda create -n YOUR_ENV_NAME python=3.8
    >
    > conda activate YOUR_ENV_NAME

- Run the command to install all dependencies
    > pip install -r requirements.txt

## File Structure
```
mov_recsys
 ┣ ml-latest-small # dataset
 ┃ ┣ links.csv
 ┃ ┣ movies.csv
 ┃ ┣ ratings.csv
 ┃ ┣ README.txt
 ┃ ┗ tags.csv
 ┣ .gitignore
 ┣ README.md
 ┣ requirements.txt
 ┣ test_user_cf.py # test modules
 ┗ user_cf.py # main fucntion for CF recommendation
```

## Dataset
These MovieLens datasets will change over time, and are not appropriate for reporting research results. I used the MovieLens-small: 100,000 ratings and 3,600 tag applications applied to 9,000 movies by 600 users, last updated 9/2018.

Download the dataset and unzip in the root of this directory:
- [MovieLens-small version](https://grouplens.org/datasets/movielens/latest/)

Well, **As the dataset is not large**, for convenience, I also **uploaded it to Github**.

## CF Method and Evaluation
User-based Collaborative Filtering, as a unsupervised method, does not learning any parameter using gradient descent (or any other optimization algorithm). Instead, it uses cosine similarity or Pearson correlation coefficients, which are only based on arithmetic operations.

## Testing on system
From the angle of software engineering, I wrote several **unit tests** on some main functions. The testing can be run by the **command** `pytest` in the main directory or use "testing" button in VScode.

## Demo Locally
The demo of system output is returned JSON values from FastAPI. Given the dependencies are installed, just run 
> uvicorn main:app --reload

in command line and turn to the Swagger UI interactive page http://127.0.0.1:8000/docs of FastAPI.
