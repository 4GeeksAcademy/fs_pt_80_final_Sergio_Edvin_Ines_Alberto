import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import "../../styles/ordersuccess.css";


export const OrderSuccess = () => {
    const { store, actions } = useContext(Context);
    const navigate = useNavigate()


    setTimeout(() => {
       navigate('/')
    }, 15000)


    return (
        <div className="order-container">
            <div className="order-card">
                 
                <div className="order-details">
                    <h5 className="order-success-title">¡Pedido realizado con éxito!</h5>
                    <p>{store.orderSuccess?.date} </p>
                    <p> <b>Subtotal:</b> {(store.orderSuccess?.total_amount / 100).toFixed(2).replace('.', ',')} € </p>
                    <p><b>Total:</b> {(store.orderSuccess?.total_amount / 100).toFixed(2).replace('.', ',')} € </p>
                    <p> <b>Descuento:</b> {store.orderSuccess?.discount} </p>
                    <p><b>Dirección:</b>{store.orderSuccess?.address} </p>
               
                        <p>{store.orderSuccess?.city}</p>
                        <p>{store.orderSuccess?.postal_code} </p>
                
                </div>
                <div>
                    <Link to="/">
                        <button className="home-button faq-home-button">
                            Home
                        </button>
                    </Link>
                </div>
            </div>
        </div>

    );
};

