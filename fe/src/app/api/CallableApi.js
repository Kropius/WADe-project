import axios from "axios";
import PubSub from "pubsub-js";
import ApiConfig from "./ApiConfig";

const CallableApi = () =>{
    // eslint-disable-next-line no-unused-vars
    const headers = {
        "X-API-Key": ApiConfig.API_KEY
    };

    function defaultSuccessHandler(response){
        console.log(`Received response: ${response}`);
        return response;
    }
    function handleError(error){
        if(error?.response){
            PubSub.publish("networkError",
                {title: "Something went wrong with your request",error: error?.response });
            return Promise.reject(error.response);
        }
        PubSub.publish("networkError", {title: "Something went wrong with your request", error:"Unknown error"} );
        return Promise.reject();
    }
    // eslint-disable-next-line no-unused-vars
    const get = async(path,params) => {
        return axios.get(path, {headers:headers, params:params})
            .then(defaultSuccessHandler)
            .catch(handleError);
    };

    const post = async(path, resource, params) => {
        return axios.post(path, resource, {
            params
        })
            .then(defaultSuccessHandler)
            .catch(handleError);
    };

    const put = async(path, resource, params) => {
        return axios.put(path,resource, {params})
            .then(defaultSuccessHandler)
            .catch(handleError);
    };

    const patch = async(path, resource, params) =>{
        return axios.patch(path,resource, {params})
            .then(defaultSuccessHandler)
            .catch(handleError);
    };

    const Delete = async(path, resource, params) =>{
        return axios.delete(path, {params})
            .then(defaultSuccessHandler)
            .catch(handleError);
    };

    const mockPost = async (path) => {
        return axios.post(path)
            .then(defaultSuccessHandler)
            .catch(handleError);
    };
    return {
        get,
        post,
        put,
        patch,
        Delete,
        mockPost
    };

};

export default CallableApi;
