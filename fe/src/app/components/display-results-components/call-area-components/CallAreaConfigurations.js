import OpenApiCalls from "../../../api/OpenApiCalls";
import PubSub from "pubsub-js";

const CallAreaConfigurations = {
    successHandler: (result) => PubSub.publish("openApiResponse", result),
    POST: (path,params) => OpenApiCalls().POST(path,params)
        .then((response)=>CallAreaConfigurations.successHandler(response))
};

export default CallAreaConfigurations;
