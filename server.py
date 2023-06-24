from hashlib import md5
from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Ads, Users
from schema import CreateAd, PathAd, CreateUser, VALIDATION_CLASS
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

app = Flask("app")



def get_ad(session: Session, id: int):
    ads = session.get(Ads, id)
    if ads is None:
        raise HttpError(404, message="Ad doesn't exist")
    return ads

def get_user(session: Session, mail: str, password: str):
    user = session.query(Users).filter_by(user_mail = mail).first()
    if user is None:
        raise HttpError(401, message="incorrect email or password")
    elif  hash_password(password=password) != user.user_password:
        raise HttpError(401, message="incorrect email or password")
    return(user)


class HttpError(Exception):
    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message



@app.errorhandler(HttpError)
def http_error_handler(error: HttpError):
    error_message = {"status": "error", "description": error.message}
    response = jsonify(error_message)
    response.status_code = error.status_code
    return response



def validate_json(json_data: dict, validation_model: VALIDATION_CLASS):
    try:
        model_obj = validation_model(**json_data)
        model_obj_dict = model_obj.dict(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, message=err.errors())
    return model_obj_dict


def hash_password(password: str):
    password = password.encode()
    password_hash = md5(password)
    password_hash_str = password_hash.hexdigest()
    return password_hash_str


class AdView(MethodView):

    def get(self, id: int):
        with Session() as session:
            ads = get_ad(session=session, id=id)
            return jsonify(
                {
                    
                    "id": ads.ad_id,
                    "title": ads.ad_title,
                    "description": ads.ad_description,
                    "creation_time": ads.ad_creation_time.isoformat(),
                    "author": ads.ad_creator,
                }
            )    


    def post(self):  
        json_data = validate_json(request.json, CreateAd)
        with Session() as session:
            ads = Ads(**json_data)
            session.add(ads)
            session.commit()
            return jsonify({"ad_id": ads.ad_id})
        


    def patch(self, id: int):
        json_data = validate_json(request.json, PathAd)
        
        with Session() as session:
            ads = get_ad(session=session, id=id)
            for field, value in json_data.items():
                setattr(ads, field, value)
            session.add(ads)
            
            session.commit()
       
            return jsonify(
                {
                    "id": ads.ad_id,
                    "title": ads.ad_title,
                    "description": ads.ad_description,
                    "creation_time": ads.ad_creation_time.isoformat(),
                    "author": ads.ad_creator,
                }
            )

    def delete(self, id: int):
        with Session() as session:
            ads = get_ad(session=session, id=id)
            session.delete(ads)
            session.commit()
            return jsonify({"status": "success"})
        




class UserView(MethodView):


    def get(self):
        print('-'*20)
        print(request.args['mail'])
        print('-'*20)
        with Session() as session:
            user = get_user(session=session, mail=request.args['mail'], password=request.args['password'])
            return jsonify(
                {
                    "id": user.user_id,
                    "email": user.user_mail,
                }
            )



    def post(self):  
        json_data = validate_json(request.json, CreateUser)
        # json_data = request.json
        json_data["user_password"] = hash_password(json_data["user_password"])
        with Session() as session:
            user = Users(**json_data)
            session.add(user)

            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, f'{json_data["user_mail"]} is busy')
            return jsonify({"id": user.user_id})





        
app.add_url_rule("/ads/", view_func=AdView.as_view("ads_view"), methods=["POST"])

app.add_url_rule(
    "/ads/<int:id>",
    view_func=AdView.as_view("with_ad_id"),
    methods=["GET", "PATCH", "DELETE"],
)


app.add_url_rule("/registration/", view_func=UserView.as_view("user_view"), methods=["POST"])

app.add_url_rule(
    "/login/",
    view_func=UserView.as_view("with_user_id"),
    methods=["GET", "PATCH", "DELETE"],
)

if __name__ == "__main__":
    app.run()