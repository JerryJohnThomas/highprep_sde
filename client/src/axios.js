import axios from  "axios";

const instance = axios.create({
    // baseURL: "https://innovationsitev2.herokuapp.com/"
    // baseURL: "https://4a20-14-139-174-50.in.ngrok.io"
    // baseURL: "https://8f1f-2409-4073-4d8e-70c9-3091-6b34-1a8f-f73c.in.ngrok.io/"
    // baseURL: "https://4040-2409-4073-4d88-b7b3-3091-6b34-1a8f-f73c.in.ngrok.io"
    // baseURL: "https://1927-27-63-208-221.in.ngrok.io"
    baseURL : "https://5acc-14-139-174-50.in.ngrok.io/"
})

export default instance;


// shubang
// axios
//                 // .get(`http://46af-14-139-174-50.in.ngrok.io/inventory/`)
//                 .get(`/inventory/`)
//                 .then((res) => {
//                     console.log(res.data);
//                     setFormState("DONE");
//                     setResultState(res.data);
//                 })
//                 .catch((error) => {
//                     setFormState("ERROR");
//                     console.log(error);
//                 });
//         }


// how to use
// type1 


//    const project_update_button_handler=(e) =>{
//        e.preventDefault();  
//        fetchData11();
//        async function fetchData11(){
//         let templink="/projects/status_update/";
//         templink+=title;
//         templink+="/";
//         templink+=opt;
//         console.log("asynnc");
//         const peq= await axios.patch(templink);
//         return peq;
//         }
//    }



// type 2
    // const handleSubmit = (e) =>{
    //     e.preventDefault();
        
    //    async function post_karo(){
    //     const peq=await axios.post(`/joel/contact/home`,{
    //       name:name,
    //       email:email,
    //       subject:contact,
    //       description:description,
    //     }).then(()=>{})
    //     .catch(err=>alert(err))
    //    }
    //     if (name.length==0)
    //         alert("enter name");
    //     else if(contact.length==0)
    //         alert("enter contact number");
    //     else if(email.length==0)
    //         alert("enter email");
    //     else if(ValidateEmail(email)==false)
    //         alert("enter Valid email");
    //     else if(description.length==0)
    //         alert("enter descrption");
    //     else
    //         {post_karo();
    //             setName("");
    //             setContact("");
    //             setEmail("");
    //             setDescription("");
    //         }

