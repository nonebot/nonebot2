---
sidebar_position: 2
description: 测试
---

# 测试

百思不如一试，测试是发现问题的最佳方式。

不同的用户会有不同的配置，为了提高项目的兼容性，我们需要在不同数据库后端上测试。
手动进行大量的、重复的测试不可靠，也不现实，因此我们推荐使用 [GitHub Actions](https://github.com/features/actions) 进行自动化测试：

```yaml title=.github/workflows/test.yml {12-42,52-53} showLineNumbers
name: Test

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        db:
          - sqlite+aiosqlite:///db.sqlite3
          - postgresql+psycopg://postgres:postgres@localhost:5432/postgres
          - mysql+aiomysql://mysql:mysql@localhost:3306/mymysql

      fail-fast: false

    env:
      SQLALCHEMY_DATABASE_URL: ${{ matrix.db }}

    services:
      postgresql:
        image: ${{ startsWith(matrix.db, 'postgresql') && 'postgres' || '' }}
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: postgres
        ports:
          - 5432:5432

      mysql:
        image: ${{ startsWith(matrix.db, 'mysql') && 'mysql' || '' }}
        env:
          MYSQL_ROOT_PASSWORD: mysql
          MYSQL_USER: mysql
          MYSQL_PASSWORD: mysql
          MYSQL_DATABASE: mymysql
        ports:
          - 3306:3306

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run migrations
        run: pipx run nb-cli orm upgrade

      - name: Run tests
        run: pytest
```

如果项目还需要考虑跨平台和跨 Python 版本兼容，测试矩阵中还需要增加这两个维度。
但是，我们没必要在所有平台和 Python 版本上运行所有数据库的测试，因为很显然，PostgreSQL 和 MySQL 这类独立的数据库后端不会受平台和 Python 影响，而且 Github Actions 的非 Linux 平台不支持运行独立服务：

|             | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12                 |
| ----------- | ---------- | ----------- | ----------- | --------------------------- |
| **Linux**   | SQLite     | SQLite      | SQLite      | SQLite / PostgreSQL / MySQL |
| **Windows** | SQLite     | SQLite      | SQLite      | SQLite                      |
| **macOS**   | SQLite     | SQLite      | SQLite      | SQLite                      |

```yaml title=.github/workflows/test.yml {12-24} showLineNumbers
name: Test

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.9", "3.10", "3.11", "3.12"]
        db: ["sqlite+aiosqlite:///db.sqlite3"]

        include:
          - os: ubuntu-latest
            python-version: "3.12"
            db: postgresql+psycopg://postgres:postgres@localhost:5432/postgres
          - os: ubuntu-latest
            python-version: "3.12"
            db: mysql+aiomysql://mysql:mysql@localhost:3306/mymysql

      fail-fast: false

    env:
      SQLALCHEMY_DATABASE_URL: ${{ matrix.db }}

    services:
      postgresql:
        image: ${{ startsWith(matrix.db, 'postgresql') && 'postgres' || '' }}
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: postgres
        ports:
          - 5432:5432

      mysql:
        image: ${{ startsWith(matrix.db, 'mysql') && 'mysql' || '' }}
        env:
          MYSQL_ROOT_PASSWORD: mysql
          MYSQL_USER: mysql
          MYSQL_PASSWORD: mysql
          MYSQL_DATABASE: mymysql
        ports:
          - 3306:3306

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run migrations
        run: pipx run nb-cli orm upgrade

      - name: Run tests
        run: pytest
```
