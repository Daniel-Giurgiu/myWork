import React, {useState, useEffect} from "react";
import Table from "./Table";
import axios from "axios";
import PostForm from "./PostForm";

function Tblu() {
    const [elem, setElem] = useState([]);
    const [isOpen, setIsOpen] = useState(false);
    const add = () => {
        setIsOpen(!isOpen);
    }
    const getElem = () => {
        axios.get('http://localhost:5000/GET')
        .then(res => {
            const elems = res.data
            setElem(elems)
        })
    }
    const deleteMe = (ID) => {
        axios.delete(`http://127.0.0.1:5000/GET/${ID}`)
            .then(res => {
            var elem = document.getElementById(ID)
            elem.remove();
            console.log(res)
            })
    }
    useEffect(() => {
        getElem()
        
    }, []);
 

    return (
        <body>
            <div>
                <div id="myDynamicTable" onClick={add}>➕</div>
                {isOpen ? <PostForm getElem={getElem} isOpen={isOpen}/> : <div></div>}
            </div>
        <table >
            <tr> 
                <th>ID</th>
                <th>Photo</th>
                <th>FirstName</th>
                <th>LastName</th>
                <th>height</th>
                <th>Delete</th>
                <th>Edit</th>
            </tr>

            {elem.map((el, i) => <Table ID={i+1} 
                id={elem[i].ID} 
                thumbnail={elem[i].thumbnail} 
                FirstName={elem[i].FirstName} 
                LastName={elem[i].LastName} 
                height={elem[i].height} 
                deleteMe={deleteMe}
                getElem={getElem}/>)
            }
            </table>
        </body>
    )
}
export default Tblu;
