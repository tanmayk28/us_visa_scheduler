class LoginError(Exception):
    pass


class SessionExpiredError(Exception):
    pass


class AccountBannedError(Exception):
    pass


class RescheduleError(Exception):
    pass
