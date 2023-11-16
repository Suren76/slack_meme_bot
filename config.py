from os import getenv

DEBUG = True

TOKEN = {
    "bot": getenv("TOKEN_BOT"),
    "user": getenv("TOKEN_USER")
}

channels = {
    "general": "C05C8D6NG9M",
    "random": "C05CNV0SN2W",
    "bot": "C05CG9W33GE",
    "parsyansuren": "D05CNRBMK6X"
}


BASE_MICROSERVICE_CONFIGS = {
    "HOST": "localhost",
    "PORT": 8080
}

SOLID_MICROSERVICE_CONFIGS = BASE_MICROSERVICE_CONFIGS.copy()


MICROSERVICE_HANDLER = {
    "HOST": SOLID_MICROSERVICE_CONFIGS["HOST"],
    "PORT": SOLID_MICROSERVICE_CONFIGS["PORT"],
    "PATH": "/handler"
}

MICROSERVICE_BOT_EVENTS = {
    "HOST": SOLID_MICROSERVICE_CONFIGS["HOST"],
    "PORT": SOLID_MICROSERVICE_CONFIGS["PORT"],
    "PATH": "/bot"
}





