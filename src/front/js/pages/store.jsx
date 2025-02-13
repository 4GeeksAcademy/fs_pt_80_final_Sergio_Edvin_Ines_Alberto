import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
import "../../styles/store.css";

import { ProductCard } from "../component/product-small-card.jsx";
import { VideogameCard } from "../component/videogame-small-card.jsx";
import { LoginModal } from "../component/login-modal.jsx";




export const Store = () => {
    const { store, actions } = useContext(Context);
    const navigate = useNavigate();

    const handleCategoryClick = (category) => {
        navigate(`/store/${category}`);
    };

    useEffect(() => {
        actions.setShowLoginModal(false); 
      }, []);
    return (
        
        <div className="home-container">
            {store.showLoginModal && <LoginModal />}
            <div className="row d-flex justify-content-center my-5 icons-store">
                <figure className="col-4 col-lg-2">
                    <img src="https://res.cloudinary.com/dshjlidcs/image/upload/c_thumb,w_200,g_face/v1738527219/web-img/vhxp03yiac2oxegzcy9a.png" alt="Consolas" onClick={() => handleCategoryClick("consolas")} className="img-fluid" />
                </figure>
                <figure className="col-4 col-lg-2">
                    <img src="https://res.cloudinary.com/dshjlidcs/image/upload/c_thumb,w_200,g_face/v1738527219/web-img/mufcnmnv4pcgs71dyhyc.png" alt="Videojuegos" onClick={() => handleCategoryClick("videojuegos")} className="img-fluid"/>
                </figure>
                <figure className="col-4 col-lg-2">
                    <img src="https://res.cloudinary.com/dshjlidcs/image/upload/c_thumb,w_200,g_face/v1738527219/web-img/ciyiiqpzbxoj2jn37kqu.png" alt="Accesorios" onClick={() => handleCategoryClick("accesories")} className="img-fluid"/>
                </figure>
            </div>
            <section className="my-5">
                <h3 className="t-seccion">Destacados</h3>
                <div className="horizontal-scrollable">
                    <div className="row flex-nowrap pt-1">
                        {store.promoted
                            ?.filter((promo) => !promo.category || promo.category !== "videojuegos")
                            .map((promo) => (
                                <ProductCard
                                    key={promo.id}
                                    img={promo.img}
                                    name={promo.name}
                                    brand={promo.brand}
                                    price={promo.price}
                                    promoted={promo.promoted}
                                    id={promo.id}
                                />
                            ))}
                    </div>
                </div>
            </section>
            <div className="divider"></div>
            <section className="my-5">
                <h3 className="t-seccion">Consolas</h3>
                <div className="horizontal-scrollable">
                    <div className="row flex-nowrap pt-1">
                        {store.consolas
                            ?.filter((console) => !console.promoted)
                            .map((console) => (
                                <ProductCard
                                    key={console.id}
                                    img={console.img}
                                    name={console.name}
                                    brand={console.brand}
                                    price={console.price}
                                    promoted={console.promoted}
                                    id={console.id}
                                />
                            ))}
                    </div>
                </div>
            </section>
            <div className="divider"></div>
            <section className="my-5">
                <h3 className="t-seccion">Destacados</h3>
                <div className="horizontal-scrollable">
                    <div className="row flex-nowrap pt-1">
                        {store.promoted
                            ?.filter((promo) => !promo.category || promo.category == "videojuegos")
                            .map((promo) => (
                                <VideogameCard
                                    key={promo.id}
                                    img={promo.img}
                                    name={promo.name}
                                    brand={promo.brand}
                                    price={promo.price}
                                    promoted={promo.promoted}
                                    id={promo.id}
                                />
                            ))}
                    </div>
                </div>
            </section>
            <div className="divider"></div>
            <section className="my-5">
                <h3 className="t-seccion">Videojuegos</h3>
                <div className="horizontal-scrollable">
                    <div className="row flex-nowrap pt-1">
                        {store.videojuegos
                            ?.filter((videogame) => !videogame.promoted)
                            .map((videogame) => (
                                <VideogameCard
                                    key={videogame.id}
                                    img={videogame.img}
                                    name={videogame.name}
                                    brand={videogame.brand}
                                    price={videogame.price}
                                    promoted={videogame.promoted}
                                    id={videogame.id}
                                />
                            ))}
                    </div>
                </div>
            </section>
            <div className="divider"></div>
            <section className="my-5">
                <h3 className="t-seccion">Accesorios</h3>
                <div className="horizontal-scrollable">
                    <div className="row flex-nowrap pt-1">
                        {store.accesorios?.filter((accesorio) => !accesorio.promoted).map((accesorio) => (
                            <ProductCard
                                key={accesorio.id}
                                img={accesorio.img}
                                name={accesorio.name}
                                brand={accesorio.brand}
                                price={accesorio.price}
                                promoted={accesorio.promoted}
                                id={accesorio.id}
                            />
                        ))}
                    </div>
                </div>
            </section>
            <div className="divider"></div>
        </div>
    );
};
