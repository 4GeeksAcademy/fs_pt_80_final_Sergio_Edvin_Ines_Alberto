import React, { Component, useContext } from "react";
import { Navigate, useNavigate } from "react-router";
import "../../styles/smallcard.css";
import { Context } from "../store/appContext";

export const ProductCard = (props) => {
  const { store, actions } = useContext(Context)
  const navigate = useNavigate();

  const isPromoted = props.promoted === true

  const handleCardClick = () => {
    navigate(`/product/${props.id}`);
  };

  const handleFav = (e) => {
    e.stopPropagation();
    if (store.user) {
      const newFav = {
        user_id: store.user.id,
        product_id: props.id,
      };
      actions.toggleFav(newFav);
    }
    else {
      const newFav = {
        product_id: props.id,
      };
      actions.toggleLocalFav(newFav);
    }
  }


  const handleShopping = () => {
    if (store.user) {
      const newShoppingItem = {
        user_id: store.user.id,
        product_id: props.id,
      };
      actions.toggleCart(newShoppingItem);
    }
    else {
      const newShoppingItem = {
        product_id: props.id,
        name: props.name,
        img: props.img,
        price: props.price,
      };
      actions.toggleLocalCart(newShoppingItem);
    }
  }

  const isFavorite = store.user
  ? store.user.favorites?.some((fav) => fav === props.id)
  : store.localFavorites?.some((fav) => fav.product_id === props.id) || false;

  const isInShopping = store.user
  ? store.shoppingCart?.some((item) => item.id === props.id)
  : store.localShoppingCart?.some((item) => item.product_id === props.id)
  return (<>
    <div className="col-10 col-md-6 col-xl-4"  >

      <div className={isPromoted ? "promoted" : "product-sm-bg"} onClick={handleCardClick}>

        <img
          className="img-fluid"
          src={props.img}
          alt={props.name}
        />
      </div>

      <div className="px-0 mt-2">
        <span className="small-c-brand" onClick={handleCardClick}>{props.brand}</span>
        <h5 className="small-c-name" onClick={handleCardClick}>{props.name}</h5>
        <div className="d-flex justify-content-between">
          <span className="small-c-price">
            {props.price !== undefined && !isNaN(props.price)
              ? `${props.price.toFixed(2)}€`
              : "N/A"}
          </span>
          <div className="d-flex align-items-center">
            <span className="fa-solid fa-plus plus-icon" style={{
              opacity: isInShopping ? 1 : 0.4,
              color: isInShopping ? "#15a3f5" : "#FFFFFF"
            }} onClick={handleShopping}></span>
            <span className="fa-solid fa-star fav-icon" style={{ opacity: isFavorite ? 1 : 0.4, }} onClick={handleFav}></span>
          </div></div>

      </div>
    </div>
  </>)
};
