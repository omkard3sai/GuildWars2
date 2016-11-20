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
        tooltip = temp['description'] + "\n"
        for fact in temp['facts']:
            if 'status' in fact:
                tooltip += "\n" + fact['status'] + ": " + fact['description']
        returndata = {
            'name': temp['name'],
            'url': temp['icon'],
            'tooltip': tooltip
        }
        return returndata

    # Get trait
    def _gettrait(self, traitid):
        temp = self._urlcall('traits', traitid)
        tooltip = temp['description'] + "\n"
        for fact in temp['facts']:
            if 'status' in fact:
                tooltip += "\n" + fact['status'] + ": " + fact['description']
        returndata = {
            'name': temp['name'],
            'url': temp['icon'],
            'tooltip': tooltip
        }
        return returndata

    # Set profession
    def _setprofession(self, profession):
        profession = self._urlcall('professions', profession)
        self._profession = {
            'weapons': profession['weapons'],
            'specializations': profession['specializations']
        }
        self._reinitweapons = True,
        self._reinitspecializations = True
        self._professiontitle = profession['name']

    # Set weapons for profession
    def _setweapons(self):
        self._weapons = dict()
        for weapon, skills in self._profession['weapons'].items():
            skilllist = list()
            for skill in skills['skills']:
                skilllist.append(self._getskill(skill['id']))
            self._weapons[weapon] = skilllist

    # Set specializations for profession
    def _setspecializations(self):
        self._specializations = dict()
        for specid in self._profession['specializations']:
            temp = self._urlcall('specializations', specid)
            traitlist = list()
            for trait in temp['major_traits'] + temp['minor_traits']:
                traitlist.append(self._gettrait(trait))
            self._specializations[temp['name']] = traitlist

    # Get profession
    def _getprofession(self):
        return self._profession

    # Get weapons for profession
    def _getweapons(self):
        if self._reinitweapons:
            self._setweapons()
            self._reinitweapons = False
        return self._weapons

    # Get specialization from a profession
    def _getspecializations(self):
        if self._reinitspecializations:
            self._setspecializations()
            self._reinitspecializations = False
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

