class LoginError(Exception):
    pass


class SessionExpiredError(Exception):
    pass


class AccountBannedError(Exception):
    pass


class NoDateError(Exception):
    pass


class RescheduleError(Exception):
    pass
