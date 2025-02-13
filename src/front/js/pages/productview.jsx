import React, { useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Context } from "../store/appContext";
import "../../styles/productview.css";

export const ProductView = () => {
    const { id } = useParams();
    const { store, actions } = useContext(Context);
    const [product, setProduct] = useState(null);
    const [rating, setRating] = useState(0);
    const [buyer, setBuyer] = useState("");

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const fetchedProduct = await actions.getProductById(id);
                if (fetchedProduct) {
                    setProduct(fetchedProduct);
                } else {
                    console.error("Producto no encontrado.");
                }
            } catch (error) {
                console.error("Error al obtener el producto:", error);
            }
        };

        const users = [
            "FinalBossStore","FinalBossStore","FinalBossStore","FinalBossStore",
            "juanito22", "CarmenEspaña", "halamadrid10", "ClassicAaron",
            "PixelAndrea", "retroLucas", "AlbertoGamer", "MarianaAdventure",
            "RaulCollector", "SofiaLover", "MartinRetro", "LauraPlays"
        ];

        const getRandomUser = () => users[Math.floor(Math.random() * users.length)];
        setBuyer(getRandomUser());

        const generateRandomRating = () => {
            const randomRating = Math.floor(Math.random() * 3) + 3;
            setRating(randomRating);
        };

        fetchProduct();
        generateRandomRating();
    }, [id]);

    const handleAddToCart = () => {
        const newShoppingItem = {
            user_id: store.user.id,
            product_id: product.id,
        };
        actions.toggleCart(newShoppingItem);
    };
    const renderStars = () => {
        let stars = "";
        for (let i = 0; i < 5; i++) {
            stars += i < rating ? "★" : "☆";
        }
        return stars;
    };

    if (!product) {
        return <p>Producto no encontrado. Por favor, verifica el ID o inténtalo más tarde.</p>;
    }

    return (
        <div className="__product_container__">
            <section className="__product_header__">
                <div className="row align-items-center">
                    <div className="col-md-6 d-flex flex-column align-items-start">
                        <p className="brand">{product.brand}</p>
                        <h1 className="__product_name__">{product.name}</h1>
                        <div className="d-flex justify-content-center mt-3">
                            <img
                                src={product.img}
                                alt={product.name}
                                className="img-fluid __product_image__"
                            />
                        </div>
                    </div>
                    <div className="col-md-6 __product_info__">
                        <div className="row">
                            <div className="col-6">
                                <p className="__info_label__">Año:</p>
                                <p className="__info_value__">{product.year}</p>
                            </div>
                            <div className="col-6">
                                <p className="__info_label__">Estado:</p>
                                <p className="__info_value__">{product.state ? "Nuevo" : "Usado"}</p>
                            </div>
                            <div className="col-12">
                                <p className="__info_label__">Plataforma:</p>
                                <p className="__info_value__">{product.platform}</p>
                            </div>
                            <div className="col-12">
                                <p className="__info_label__">Tipo:</p>
                                <p className="__info_value__">{product.type}</p>
                            </div>
                            <div className="col-12 d-flex align-items-start mb-4">
                                <p className="__info_label__">Vendido por:</p>
                                <div className="d-flex align-items-col ms-2">
                                    <img
                                        src={"https://res.cloudinary.com/dshjlidcs/image/upload/v1738526760/t9wliafde7eongd3umez-min_usjcnx.png"}
                                        className="__seller_avatar__"
                                    />
                                    <span className="ms-2">{buyer}</span>
                                </div>
                            </div>
                            <div className="col-12 d-flex justify-content-between align-items-center">
                                <span className="rating">{renderStars()}</span>
                                <div className="product-price">
                                    <p className="__price_value__">{product.price.toFixed(2)}€</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section className="__product_description__ mt-4">
                <div className="row">
                    <div className="col-12">
                        <p>{product.description}</p>
                    </div>
                </div>
            </section>

            <section className="__product_button__ mt-4">
                <div className="row">
                    <div className="col-12 d-flex justify-content-center">
                        <button className="btn btn-warning" onClick={handleAddToCart}>
                            Comprar
                        </button>
                    </div>
                </div>
            </section>
        </div>
    );
};