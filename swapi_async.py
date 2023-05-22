import asyncio
import aiohttp
import datetime
import requests

from models import engine, Session, Base, SwapiPeople


async def get_people(page):
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"https://swapi.dev/api/people/?page={page}")
        json_data = await response.json()
    return json_data["results"]


async def fetch_data(session, url):
    async with session.get(url) as response:
        data = await response.json()
        return data


async def get_films(session, films):
    films_data = await asyncio.gather(
        *[fetch_data(session, film_url) for film_url in films]
    )
    return ",".join([film_data["title"] for film_data in films_data])


async def get_species(session, species):
    species_data = await asyncio.gather(
        *[fetch_data(session, species_url) for species_url in species]
    )
    return ",".join([species_data["name"] for species_data in species_data])


async def get_starships(session, starships):
    starships_data = await asyncio.gather(
        *[fetch_data(session, starship_url) for starship_url in starships]
    )
    return ",".join([starship_data["name"] for starship_data in starships_data])


async def get_vehicles(session, vehicles):
    vehicles_data = await asyncio.gather(
        *[fetch_data(session, vehicle_url) for vehicle_url in vehicles]
    )
    return ",".join([vehicle_data["name"] for vehicle_data in vehicles_data])


async def get_homeworld(session, homeworld):
    homeworld_data = await asyncio.gather(fetch_data(session, homeworld))
    return homeworld_data[0]["name"]


async def paste_to_db(persons_jsons):
    async with Session() as session:
        orm_objects = []
        async with aiohttp.ClientSession() as http_session:
            for item in persons_jsons:
                films = await get_films(http_session, item["films"])
                species = await get_species(http_session, item["species"])
                starships = await get_starships(http_session, item["starships"])
                vehicles = await get_vehicles(http_session, item["vehicles"])
                homeworld = await get_homeworld(http_session, item["homeworld"])
                orm_object = SwapiPeople(
                    birth_year=item["birth_year"],
                    eye_color=item["eye_color"],
                    films=films,
                    gender=item["gender"],
                    hair_color=item["hair_color"],
                    height=item["height"],
                    homeworld=homeworld,
                    mass=item["mass"],
                    name=item["name"],
                    skin_color=item["skin_color"],
                    species=species,
                    starships=starships,
                    vehicles=vehicles,
                )
                orm_objects.append(orm_object)
                print(
                    orm_object.name,
                    orm_object.homeworld,
                )

        async with Session() as db_session:
            db_session.add_all(orm_objects)
            await db_session.commit()


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    pages = requests.get("https://swapi.dev/api/people/").json()["count"] // 10 + 1
    person_coros = [get_people(i) for i in range(1, pages + 1)]
    tasks = []
    for person_coro in person_coros:
        persons = await person_coro
        task = asyncio.create_task(paste_to_db(persons))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
