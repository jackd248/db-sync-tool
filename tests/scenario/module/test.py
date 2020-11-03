import db_sync_tool

if __name__ == "__main__":
    db_sync_tool.Sync({
        'verbose': False,
        'mute': True
    }, {
        "name": "project",
        "type": "TYPO3",
        "target": {
            "path": "/var/www/html/tests/files/www2/LocalConfiguration.php"
        },
        "origin": {
            "host": "www1",
            "user": "user",
            "password": "password",
            "path": "/var/www/html/tests/files/www1/LocalConfiguration.php"
        },
        "ignore_table": []
    })
