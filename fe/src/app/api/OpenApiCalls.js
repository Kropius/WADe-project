import CallableApi from "./CallableApi";
import PubSub from "pubsub-js";

const OpenApiCalls = () =>{
    const POST = async(path, resource, params) =>{
        return CallableApi().post(path,resource, params)
            .then((response) =>PubSub.publish("openApiResponse",response));
    };
    const GET = async(path, params) =>{
        return CallableApi().get(path, params)
            .then((response) =>PubSub.publish("openApiResponse",response));
    };
    const PUT = async(path, resource, params) =>{
        return CallableApi().put(path,resource, params)
            .then((response) =>PubSub.publish("openApiResponse",response));
    };
    const PATCH = async(path, resource, params) =>{
        return CallableApi().patch(path,resource, params)
            .then((response) =>PubSub.publish("openApiResponse",response));
    };
    const DELETE = async(path, params) =>{
        return CallableApi().delete(path, params)
            .then((response) =>PubSub.publish("openApiResponse",response));
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
