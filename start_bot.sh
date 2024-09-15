#!/bin/bash
echo "Alembic upgrade"
alembic upgrade head
echo "Combot start"
combot