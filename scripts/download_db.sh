#!/bin/sh

file_id="1XUJj_daYch9DvMlnw7j9IkF_G1Vaz2zU"

wget --no-check-certificate "https://docs.google.com/uc?export=download&id=${file_id}" -O ../databases/books.db

