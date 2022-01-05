"""Application containers module."""

from flask.templating import Environment
from dependency_injector import containers, providers
from dependency_injector.ext import flask
from flask import Flask
from flask_bootstrap import Bootstrap
from github import Github

from . import services, views


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    app = flask.Application(Flask, __name__)

    bootstrap = flask.Extension(Bootstrap)

    config = providers.Configuration()

    github_client = providers.Factory(
        Github,
        login_or_token=config.github.auth_token,
        timeout=config.github.request_timeout,
    )

    env = providers.Factory(
        services.Enviroment,
        env=config.env
    )

    search_service = providers.Factory(
        services.SearchService,
        github_client=github_client,
    )

    index_view = flask.View(
        views.index,
        search_service=search_service,
        default_query=config.search.default_query,
        default_limit=config.search.default_limit,
    )

    health_view = flask.View(
        views.healt,
        enviroment=env
    )