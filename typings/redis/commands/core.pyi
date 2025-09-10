class ManagementCommands:
    def ping(self, message: str | None = None) -> bool:
        """
        Ping the Redis server

        For more information see https://redis.io/commands/ping
        """

    def time(self) -> tuple[int, int]:
        """
        Returns the server time as a 2-item tuple of ints:
        (seconds since epoch, microseconds into this second).

        For more information see https://redis.io/commands/time
        """
