import CallableApi from "./CallableApi";
// import PubSub from "pubsub-js";

const OpenApiCalls = () =>{
    const POST = async(path, params, resource) =>{
        return CallableApi().post(path, params, resource);
            // .then((response) =>PubSub.publish("openApiResponse",response));
    };
    // eslint-disable-next-line no-unused-vars
    const GET = async(path, params, resource) =>{
        return CallableApi().get(path, params);
            // .then((response) =>PubSub.publish("openApiResponse",response));
    };
    const PUT = async(path, params, resource) =>{
        return CallableApi().put(path, params, resource);
            // .then((response) =>PubSub.publish("openApiResponse",response));
    };
    const PATCH = async(path, params, resource) =>{
        return CallableApi().patch(path, params, resource);
            // .then((response) =>PubSub.publish("openApiResponse",response));
    };
    // eslint-disable-next-line no-unused-vars
    const DELETE = async(path, params, resource) =>{
        return CallableApi().Delete(path, params);
    };
    return {
        POST,
        GET,
        PUT,
        PATCH,
        DELETE
    };
};

export default OpenApiCalls;
