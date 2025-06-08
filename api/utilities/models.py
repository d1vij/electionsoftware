from pydantic import BaseModel


class Vote(BaseModel):
    name: str
    post: str


class VoteResponse(BaseModel) :
    token: str 
    vote_data: list[Vote]
    """
    {
      "token": "1231asiodjao",
      "vote_data": [
        {
          "name": "divij",
          "post": "head_boy"
        },
        {
          "name": "abc",
          "post": "head_girl"
        }
      ]
    }
    """