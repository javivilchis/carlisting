class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    # This is where you would query your DB for the user by ID
    return User(user_id)