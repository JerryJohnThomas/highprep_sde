import axios from  "axios";

const instance = axios.create({
    // baseURL: "https://innovationsitev2.herokuapp.com/"
    // baseURL : "https://giant-ads-walk-14-139-174-50.loca.lt/",
    // baseURL: "https://short-mugs-double-14-139-174-50.loca.lt/"
    // baseURL: "https://sad-suns-see-14-139-174-50.loca.lt/"
    // baseURL: "https://short-trees-attend-14-139-174-50.loca.lt/",
    // baseURL: "https://many-mails-brush-14-139-174-50.loca.lt/"
    // baseURL: "https://9f5b-2409-4073-2e8b-dfa5-c4cc-47b2-91a4-3be2.in.ngrok.io/"
    // baseURL: "https://b699-2409-4073-48b-d532-c4cc-47b2-91a4-3be2.in.ngrok.io/"
    // baseURL: "https://5844-2401-4900-6277-ece3-c4cc-47b2-91a4-3be2.in.ngrok.io/"
    baseURL: "https://a264-2409-40f4-39-b8a6-c4cc-47b2-91a4-3be2.in.ngrok.io/"
    
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

