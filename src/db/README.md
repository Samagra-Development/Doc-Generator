## Autogeneration of ERDiagram of Database

 - Install Graphiz
   - On ubuntu you can install it using command
       ```shell
       $ sudo apt-get install graphviz libgraphviz-dev graphviz-dev pkg-config
       ```
  
 - Install PyGraphiz using following command:
   ```shell
       $ pip3 install pygraphiz
   ```
   
 - Install ERAlchemy using following command:
   ```shell
   $ pip3 install eralchemy
    ```
 - For generating ERDiagram go to the src folder and run  following command:
   ```shell
   $ python3 -m utils.generatedb-er
   ```
## Hasura ( For PSQL Database Auto api )
 - Hasura setup automatically done through docker-compose.yml of project and for [manually install hasura](https://hasura.io/docs/1.0/graphql/manual/deployment/docker/index.html#deployment-docker) 
 - You can access hasura api on localhost at "localhost:8080/v1/graphql"
 - For fetching data we have to paas query in json format as post parameter
    ```shell
     {"query":"query MyQuery {
        tablename {
            col1
            col2
            col3
         
        }
      }"
  }
   ```
   
 - [Read more about Queries](https://hasura.io/docs/1.0/graphql/manual/queries/index.html)

 