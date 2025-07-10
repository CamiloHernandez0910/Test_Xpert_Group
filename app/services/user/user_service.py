from app.core.security import verify_password, create_access_token, hash_password

class UserService:

    @staticmethod
    async def authenticate_user(username: str, password: str, db):
        user = await db["users"].find_one({
            "$or": [{"username": username}, {"email": username}]
        })
        if not user or not verify_password(password, user["password"]):
            return None
        token = create_access_token({"sub": user["email"]})
        return {
            "access_token": token,
            "token_type": "bearer",
            "username": user["username"],
            "email": user["email"]
        }

    @staticmethod
    async def create_user(user_data, db):
        users = db["users"]
        base_username = f"{user_data.name.lower()}.{user_data.last_name.lower()}"
        username, suffix = base_username, 1
        while await users.find_one({"username": username}):
            username = f"{base_username}{suffix}"
            suffix += 1

        if await users.find_one({"email": user_data.email}):
            raise ValueError("Email already registered")

        hashed_pw = hash_password(user_data.password)
        user_doc = {
            "name": user_data.name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "password": hashed_pw,
            "username": username,
        }
        result = await users.insert_one(user_doc)
        token = create_access_token({"sub": user_data.email})
        return {
            "id": str(result.inserted_id),
            "name": user_data.name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "username": username,
            "token": token           
        }

    @staticmethod
    async def get_all_users(db):
        users = db["users"]
        cursor = users.find({}, {
            "_id": 1, "name": 1, "last_name": 1, "email": 1, "username": 1
        })
        return [{
            "id": str(user["_id"]),
            "name": user["name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "username": user["username"]
        } async for user in cursor]
