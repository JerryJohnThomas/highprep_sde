import React, { useEffect, useState } from "react";

function Test() {
    const [a, b] = useState([
        [0, 1],
        [2, 3],
    ]);
    useEffect(() => {
    }, []);
    
    
    let add = () => {
        b((old) => [...old, ["test","ok"]]);
    }
    
    let add_last = () =>{
        b([...a.slice(0,-1), [...a[a.length - 1], 7]]);
    }

    let see = () =>{
        console.log(a);
    }

    let see_last = () =>{
        let temp = a[a.length - 1];
        console.log(temp[temp.length - 1]);
    }
    return (
        <>
            <div>Test</div>
            <div onClick={() => add()}>add Fresh</div>
            <div onClick={() => add_last()}>add to last</div>
            <div onClick={() => see()}>see</div>
            <div onClick={() => see_last()}>see last[last]</div>
        </>
    );
}

export default Test;
