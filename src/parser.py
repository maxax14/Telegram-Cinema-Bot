from kinopoisk import movie
from src import config


class Parser:
    def __init__(self):
        self.output = ""
        self.full_output = ""
        self.photo = None
        self.name = ""
        self.id = 1

    def parse_text(self, text):
        Parser.__init__(self)
        m = movie.Movie()
        movie_list = m.objects.search(text)
        if len(movie_list) == 0:
            return config.err_msg(text)
        output_text = "По запросу \"{}\" найдено:\n".format(text)
        for item in movie_list[:8]:
            title = item.title
            year = item.year
            rating = item.rating
            id = item.id
            if item.series:
                title = title + " (сериал)\t"
            if item.title_en:
                title = title + " ({})".format(item.title_en)
            if rating is None:
                rating = "Нет данных"
            output_text += "● {}\n📅: {}\t⭐️ {}\t/i{} ️\n".format(title, year, rating, id)
        return output_text

    # "● Криминальное чтиво [1995; /i342]"

    def parse_id(self, film_id):
        mov = movie.Movie(id=film_id)
        mov.get_content("main_page")
        mov.get_content("posters")
        mov.get_content("trailers")
        # Title
        title = "{}".format(mov.title)
        self.name = title
        self.id = film_id
        if mov.series:
            title += " (сериал)"
        self.full_output = title + '\n'
        year = mov.year
        genre = mov.genres[0]
        countries = mov.countries[0]
        self.output = title + ",\t [{}, {}, {}] \n".format(year, genre, countries)
        if mov.title_en:
            self.output += "\t({})\n".format(mov.title_en)
            self.full_output += "\t({})\n".format(mov.title_en)
        # Tagline
        if len(mov.tagline) > 0:
            self.full_output += "📢 {}\n".format(mov.tagline)
        # Rating
        if mov.rating is not None:
            self.output += "⭐️ {}\n".format(mov.rating)
            self.full_output += "⭐️ {}\n".format(mov.rating)
        # Date
        if mov.year is not None:
            self.full_output += "📅️ {}\n".format(mov.year)
        # Duration
        if mov.runtime is not None:
            self.output += "⏱️ {} мин.\n".format(mov.runtime)
            self.full_output += "⏱️ {} мин.\n".format(mov.runtime)
        # Genres
        if len(mov.genres) > 0:
            genres = ", ".join(mov.genres)
            self.full_output += "🎭 {}\n".format(genres)
        # Countries
        if len(mov.countries) > 0:
            countries = ", ".join(mov.countries)
            self.full_output += "🌍 {}\n".format(countries)
        # Actors
        if len(mov.actors):
            actors = ', '.join(map(lambda x: x.name, mov.actors))
            self.full_output += "👥 {}\n".format(actors)
            actors = ', '.join(map(lambda x: x.name, mov.actors[:3]))
            self.output += "👥 {}, ...\n".format(actors)
        # Directors
        if len(mov.directors) > 0:
            directors = ", ".join(map(lambda x: x.name, mov.directors))
            self.full_output += "🎬 {}\n".format(directors)
        # Composers
        if len(mov.composers) > 0:
            composers = ", ".join(map(lambda x: x.name, mov.composers))
            self.full_output += "🎵 {}\n".format(composers)
        if len(mov.trailers) > 0:
            trailer = mov.trailers[0].file
            self.output += "🎥 Посмотреть [трейлер]({}).\n".format("https://www.kinopoisk.ru/{}".format(trailer))
            self.full_output += "🎥 Посмотреть [трейлер]({}).\n".format("https://www.kinopoisk.ru/{}".format(trailer))
        # Plot
        if len(mov.plot) > 0:
            plot = ". ".join(mov.plot.split('.'))
            self.full_output += "📖 {}\n".format(plot)
            plot = ". ".join(mov.plot.split('.')[:2])
            self.output += "📖 {} ...\n".format(plot)
        if len(mov.url) > 0:
            self.output += "Страница на [Кинопоиске]({})".format(mov.url)
            self.full_output += "Страница на [Кинопоиске]({})".format(mov.url)
        # Poster
        if len(mov.posters) > 0:
            self.photo = mov.posters[0]


if __name__ == '__main__':
    pass
