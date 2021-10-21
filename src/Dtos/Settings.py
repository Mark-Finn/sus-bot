class Settings:

    def __init__(self,
                 impostors=1,
                 confirm_ejects=1,
                 emergency_meetings=1,
                 emergency_cooldown=15,
                 discussion_time=15,
                 voting_time=45,
                 kill_cooldown=45,
                 common_tasks=1,
                 long_tasks=1,
                 short_tasks=2,
                 anonymous_voting=0,
                 task_bar_updates=2, # 0 Never, 1 Meetings, 2 Always
                 sabotage_cooldown=30,
                 meltdown_time=50,
                 hypoxia_time=50,
                 ):
        self.impostors = int(impostors)
        self.confirm_ejects = int(confirm_ejects)
        self.emergency_meetings = int(emergency_meetings)
        self.emergency_cooldown = int(emergency_cooldown)
        self.discussion_time = int(discussion_time)
        self.voting_time = int(voting_time)
        self.kill_cooldown = int(kill_cooldown)
        self.common_tasks = int(common_tasks)
        self.long_tasks = int(long_tasks)
        self.short_tasks = int(short_tasks)
        self.anonymous_voting = int(anonymous_voting)
        self.task_bar_updates = int(task_bar_updates)
        self.sabotage_cooldown = int(sabotage_cooldown)
        self.meltdown_time = int(meltdown_time)
        self.hypoxia_time = int(hypoxia_time)
