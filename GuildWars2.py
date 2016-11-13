import requests


class GuildWars2:

    """

        ~~~~~  PRIVATE METHODS  ~~~~~

    """
    # API call
    @classmethod
    def _urlcall(cls, category=None, value=None):
        parameters = {'lang': 'en-US'}
        url = "https://api.guildwars2.com/v2/" + str(category)
        if value:
            url += '/' + str(value)
        return requests.get(url, params=parameters).json()

    # Get all professions
    def _getallprofessions(self):
        returndata = list()
        professionlist = self._urlcall('professions')
        for item in professionlist:
            profession = self._urlcall('professions', item)
            returndata.append({
                'name': item,
                'url': profession['icon_big']
            })
        return returndata

    # Get skill
    def _getskill(self, skillid):
        temp = self._urlcall('skills', skillid)
        returndata = {
            'name': temp['name'],
            'url': temp['icon']
        }
        return returndata

    # Set profession
    def _setprofession(self, profession):
        profession = self._urlcall('professions', profession)
        self._setspecializations(profession['specializations'])
        self._setweapons(profession['weapons'])
        self._profession = profession['name']

    # Set weapons for profession
    def _setweapons(self, weapons):
        self._weapons = list()
        for weapon, skills in weapons.items():
            skilllist = list()
            for skill in skills['skills']:
                skilllist.append(self._getskill(skill['id']))
            self._weapons.append({
                'name': weapon,
                'skills': skilllist
            })

    # Set specializations for profession
    def _setspecializations(self, specializations):
        self._specializations = list()
        for specid in specializations:
            temp = self._urlcall('specializations', specid)
            self._specializations.append({
                'name': temp['name'],
                'url': temp['icon']
            })

    # Get profession
    def _getprofession(self):
        return self._profession

    # Get weapons for profession
    def _getweapons(self):
        return self._weapons

    # Get specialization from a profession
    def _getspecializations(self):
        return self._specializations

    """

        ~~~~~  PUBLIC METHODS  ~~~~~

    """
    def setprofession(self, profession):
        self._setprofession(profession)

    def getprofession(self):
        return self._getprofession()

    def getallprofessions(self):
        return self._getallprofessions()

    def getweapons(self):
        return self._getweapons()

    def getspecializations(self):
        return self._getspecializations()
