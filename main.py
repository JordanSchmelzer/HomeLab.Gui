from Controller.app_controller import AppController


if __name__ == "__main__":
  # Dependency Inject Services
  
  app: AppController = AppController()
  app.run()
  