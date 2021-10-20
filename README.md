# KafkaCLIapp
Command-line driven program that allows message exchange.

# Dependencies
To install dependencies run command ``` pip install -r requirements.txt ```

# List of dependencies

1. attrs==21.2.0
2. confluent-kafka==1.7.0
3. coverage==6.0.2
4. iniconfig==1.1.1
5. packaging==21.0
6. pluggy==1.0.0
7. py==1.10.0
8. pyparsing==2.4.7
9. pytest==6.2.5
10. pytest-cov==3.0.0
11. toml==0.10.2
12. tomli==1.2.1

# Important to note
Apache Kafka and zookeeper should be installed on your machine. 
Create a topic of which the producer shall send messages to and consumer receive messages from. This can be done using the command below

```$ bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092 --partition 1 --replication-factor 1```

More information can be got from http://kafka.apache.org/documentation/#quickstart
