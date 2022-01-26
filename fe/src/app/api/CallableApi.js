import axios from "axios";

const CallableApi = () =>{
    function defaultSuccessHandler(response){
        console.log(`Received response: ${response}`);
        return response;
    }
    function handleError(error){
        console.log(error.toJSON());
        if(error?.response){
            return Promise.reject(error.response);
        }
        return Promise.reject({error:" Unknown error"});
    }
    const get = async(path) => {
        return axios.get(path)
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
    const mockPost = async (path) => {
        return axios.post(path)
            .then(defaultSuccessHandler)
            .catch(handleError);
    };
    return {
        get,
        post,
        mockPost
    };

};

export default CallableApi;
