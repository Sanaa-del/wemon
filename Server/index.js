const mongo = require('mongodb');

const Metrics = require('./model/metrics');

const MongoClient = mongo.MongoClient;

const url = 'mongodb://localhost:27017';

const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
// const metrics = require('./routes/routing')

const cors = require('cors');

const app = express();

let dbConnection;

MongoClient.connect(url, { useNewUrlParser: true }, (err, client) => {

    if (err) throw err;
    dbConnection = client.db("LWIP");

    dbConnection.listCollections().toArray().then((docs) => {

        console.log('Available collections:');
        docs.forEach((doc) => { console.log(doc.name) });

    }).catch((err) => {
        console.log(err);
    })
});

app.use(morgan('dev'));
app.use(bodyParser.json({ limit: '200mb', extended: true }));
app.use(bodyParser.urlencoded({ limit: '200mb', extended: true }));

app.use(cors({ origin: "*" }));

app.get('/metrics', function (req, res) {
    res.send(req.params);
});

app.post('/metrics', (req, res) => {
    const networkInfo = req.body.find(element => !!element.downlink);
    const scenarioID = req.body.find(element => !!element.ID);
    console.log('this is the id:');
    console.log(scenarioID);
    const webInfo = Object.assign({}, req.body.find(element => !!element.protocol), req.body.find(element => !!element.RUMSpeedIndex));
    const systemInfo = req.body.find(element => !!element.systemCapacity)
    const cpuInfo = req.body.find(element => !!element.cpuName)
    let metrics = new Metrics({ scenario: 'normal Scenario', cpuInfo, systemInfo, webInfo,networkInfo, scenarioID });

    dbConnection
        .collection("Metrics")
        .insertOne(metrics, function (err, result) {
            if (err) {
                res.status(400).send("Error inserting document!");
            } else {
                console.log(`Added a new document with id ` + metrics._id);
                res.status(204).send(metrics.body);
            }
        });
})

const port = process.env.PORT || 8000;

app.listen(port, () => {
    console.log(`Server is running on port ${port}`)
})
