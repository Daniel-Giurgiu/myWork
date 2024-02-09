import React, {useState} from "react";
import PutForm from "./PutForm";
import Popup from "./Popup";
import "./style.css";

function Table({ID, id, thumbnail, FirstName, LastName, height, deleteMe, getElem}){
    const [isOpen, setIsOpen] = useState(false);
    const [deleteOpen, setdeleteOpen] = useState(false);
    const [deleteClick, setdeleteClick] = useState(false);
    const deleteToggle = () => {
        setdeleteOpen(!deleteOpen);
    }
    const deleteAmu = () => {
        setdeleteClick(!deleteClick)
    }
    const togglePopup = () => {
        setIsOpen(!isOpen);
    }
    let thub = thumbnail
    let source = "/imag/" + thub
    return (
        <tr id={id} >
            <td >{ID}</td> 
            <td><img src={source} alt=""/></td>
            <td >{FirstName }</td>
            <td >{LastName }</td>
            <td >{height}</td>
    
            <td>
                <button onClick={deleteToggle} >🗑</button>
                {deleteOpen ? <Popup 
                content={<>
                    <div>
                        <p>Are you sure??</p>
                        <button onClick={deleteAmu}>Delete</button>
                    </div>
                    </>} 
                    handleClose={deleteToggle}
                    /> : <div></div>}
                {deleteClick ? deleteMe(id) : <div></div>}
            </td>
            <td>
                <button onClick={togglePopup} >📝</button>
                {isOpen ? <PutForm getElem={getElem} 
                            id={id} 
                            FirstName={FirstName} 
                            LastName={LastName} 
                            height={height}
                            photo ={thumbnail}/> : <div></div> }
            </td>
        </tr>   
    )
}

export default Table;