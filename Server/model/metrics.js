const mongoose = require('mongoose');
const { ObjectId } = mongoose.Schema;

const metricsSchema = new mongoose.Schema(
    {
        _id: {
            type: ObjectId
        },
        scenario: {
            type: String
        },
        networkInfo: {
            type: Object
        },
        cpuInfo: {
            type: Object
        },
        systemInfo:{
            type: Object
        },
        webInfo: 
        {
            type: Object
        },
        scenarioID: 
        {
            type: Object
        }
    },
    { timestamps: true }
);

module.exports = mongoose.model('Metrics', metricsSchema);
