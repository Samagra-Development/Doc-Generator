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
