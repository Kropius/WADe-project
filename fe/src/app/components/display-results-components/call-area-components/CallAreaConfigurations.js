import OpenApiCalls from "../../../api/OpenApiCalls";
import PubSub from "pubsub-js";

const CallAreaConfigurations = {
    successHandler: (result) => PubSub.publish("openApiResponse", result),
    CALLS : {
        POST: (path,params, resource) => OpenApiCalls().POST(path,params, resource)
            .then((response)=>CallAreaConfigurations.successHandler(response)),
        GET: (path,params) => OpenApiCalls().GET(path,params)
            .then((response)=>CallAreaConfigurations.successHandler(response)),
        PUT: (path,params, resource) => OpenApiCalls().PUT(path,params, resource)
            .then((response)=>CallAreaConfigurations.successHandler(response)),
        PATCH: (path,params, resource) => OpenApiCalls().PATCH(path,params, resource)
            .then((response)=>CallAreaConfigurations.successHandler(response)),
        DELETE: (path,params, resource) => OpenApiCalls().DELETE(path,params, resource)
            .then((response)=>CallAreaConfigurations.successHandler(response))

    },

    performCall: (verb, path, params, resource) => {
        if(!Object.keys(CallAreaConfigurations.CALLS).includes(verb.toUpperCase())){
            console.log("Unkown verb");
            return;
        }
        return CallAreaConfigurations.CALLS[verb.toUpperCase()](path, params, resource);
    },
};

export default CallAreaConfigurations;
