#### For development:
``` $ find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs sudo rm -rf ```

``` $ chmod +x src/entrypoint.sh ```

``` $ docker-compose up ```

### Run tests:
In separate tab

``` $ docker-compose exec django bash ``` - get into django container

``` $ $test ``` - run all tests
``