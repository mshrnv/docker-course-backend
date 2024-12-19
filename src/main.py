import asyncio
import logging
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from project.core.config import settings
from project.api.program_router import program_router
from project.api.hosts_router import host_router
from project.api.albums_router import albums_router
from project.api.artists_router import artists_router
from project.api.genres_router import genres_router
from project.api.playlist_track_router import playlist_and_track_pair_router
from project.api.playlists_router import playlists_router
from project.api.song_requests_router import song_requests_router
from project.api.tracks_router import tracks_router
from project.api.host_program_router import host_program_pair_router
from project.api.user_router import user_router

from project.api.auth_router import auth_router


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app_options = {}
    if settings.ENV.lower() == "prod":
        app_options = {
            "docs_url": None,
            "redoc_url": None,
        }
    if settings.LOG_LEVEL in ["DEBUG", "INFO"]:
        app_options["debug"] = True

    app = FastAPI(root_path=settings.ROOT_PATH, **app_options)
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(program_router, tags=["Program"])
    app.include_router(host_router, tags=["Host"])
    app.include_router(host_program_pair_router, tags=["HostProgramPair"])
    app.include_router(genres_router, tags=["Genre"])
    app.include_router(artists_router, tags=["Artist"])
    app.include_router(tracks_router, tags=["Track"])
    app.include_router(albums_router, tags=["Album"])
    app.include_router(song_requests_router, tags=["SongRequest"])
    app.include_router(playlists_router, tags=["Playlist"])
    app.include_router(playlist_and_track_pair_router, tags=["PlaylistAndTrackPair"])
    app.include_router(user_router, tags=["User"])
    app.include_router(auth_router, tags=["Auth"])

    return app


app = create_app()


async def run() -> None:
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    logger.debug(f"{settings.postgres_url}=")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())