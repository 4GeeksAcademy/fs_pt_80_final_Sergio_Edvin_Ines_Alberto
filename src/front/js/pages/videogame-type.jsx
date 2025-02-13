import React, { useContext, useEffect} from "react";
import { Context } from "../store/appContext.js";
import { useParams } from "react-router";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import "../../styles/store.css";

import { ProductBCard } from "../component/product-big-card.jsx"
import { VideogameCard } from "../component/videogame-small-card.jsx";
import {AllType} from "../component/all-type.jsx"


export const VideogameType = () => {
    const { store, actions } = useContext(Context);
    const { category } = "videojuegos";
    const { type } = useParams();
    const navigate = useNavigate();

    const handleCategoryClick = (category) => {
        navigate(`/store/${category}`);
    };

    useEffect(() => {
        window.scrollTo(0, 0); 
    }, [type]);

    return (
        <div className="home-container">
            <div className="row d-flex justify-content-center my-5 icons-store">
                <figure className="col-4 col-lg-2">
                    <img src="https://res.cloudinary.com/dshjlidcs/image/upload/c_thumb,w_200,g_face/v1738527219/web-img/vhxp03yiac2oxegzcy9a.png" alt="Consolas" className="img-fluid" onClick={() => handleCategoryClick("consolas")} />
                </figure>
                <figure className="col-4 col-lg-2">
                    <img src="https://res.cloudinary.com/dshjlidcs/image/upload/c_thumb,w_200,g_face/v1738527219/web-img/mufcnmnv4pcgs71dyhyc.png" alt="Videojuegos" className="selected img-fluid" onClick={() => handleCategoryClick("videojuegos")} />
                </figure>
                <figure className="col-4 col-lg-2">
                    <img src="https://res.cloudinary.com/dshjlidcs/image/upload/c_thumb,w_200,g_face/v1738527219/web-img/ciyiiqpzbxoj2jn37kqu.png" alt="Accesorios" className="img-fluid" onClick={() => handleCategoryClick("accesorios")} />
                </figure>
            </div>
            <h3 className="t-seccion">{type}</h3>
            <section className="my-5">
                <div className="horizontal-scrollable">
                    <div className="row flex-nowrap pt-1">
                        {
                            store.videojuegos?.filter((item) => item.type.toLowerCase() === type.toLowerCase())
                                .map((item) => (
                                    <VideogameCard
                                        key={item.id}
                                        img={item.img}
                                        name={item.name}
                                        brand={item.brand}
                                        price={item.price}
                                        promoted={item.promoted}
                                        id={item.id}
                                    />
                                ))
                        }
                    </div>
                </div>
            </section>
            <div className="divider"></div>
                        <section className="my-5">
                            <div className="pt-1">
                                {store.videojuegos
                                    ?.filter((item) => item.promoted && item.type.toLowerCase() === type.toLowerCase()).sort(() => Math.random() - 0.5).slice(0, 1)
                                    .map((item) => (
                                        <ProductBCard
                                            key={item.id}
                                            img={item.img}
                                            name={item.name}
                                            brand={item.brand}
                                            price={item.price}
                                            promoted={item.promoted}
                                            id={item.id}
                                        />
                                    ))}
                            </div>
                        </section>
                        <div className="divider"></div>
                        <section className="my-5"> 
                            <AllType/>
                        </section>
        </div>

    );
};
