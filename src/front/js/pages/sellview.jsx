import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/sellview.css";
import { useNavigate } from "react-router-dom";
import { PhotoUpload } from "../component/photoupload.jsx";
import { LoginModal } from "../component/login-modal.jsx";
import { PremiumModal } from "../component/premium-modal.jsx";


//import { LoginModal } from "../component/login-modal.jsx";

export const SellView = () => {
    const { store, actions } = useContext(Context);
    const [typeOptions, setTypeOptions] = useState([]);
    const navigate = useNavigate();
    const [uploadedPhoto, setUploadedPhoto] = useState("");
    const [showSuccess, setShowSuccess] = useState(false);


    const [formData, setFormData] = useState({
        name: "",
        description: "",
        img: "",
        year: "",
        brand: "",
        platform: "",
        type: "",
        category: "",
        state: false,
        promoted: false,
        price: "",
        seller_id: store.user.id, // User autenticado como vendedor
    });


    // Función opciones de "Tipo" según categoría seleccionada
    const updateTypeOptions = (category) => {
        setFormData({ ...formData, category, type: "" });
        setTypeOptions(
            category === "consolas" 
                ? ["Sobremesa", "Portátil", "Híbrida"] 
                : category === "videojuegos" 
                ? ["Acción", "Aventura", "Rol", "Estrategia", "Deportes", "Peleas", "Plataformas", "Terror", "Indie"] 
                : category === "accesorios" ? ["Accesorios"] : []
        );
    };

    const handleGoToPremium = () => {
        navigate("/suscripcion");
    };


    const handleImageUpload = (imageUrl) => {
        setUploadedPhoto(imageUrl);
        setFormData((prev) => ({ ...prev, img: imageUrl }));
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: name === "state" || name === "promoted" ? value === "true" : value,
        });
    };
    const validateForm = () => {
        const { name, description, img, year, brand, platform, type, category, price } = formData;

        if (!name || !description || !img || !year || !brand || !platform || !category || !type || !price) {
            alert("No olvides subir la foto del producto o completar todos los campos ⚠️");
            return false;
        }
        return true;
    };

    const handleSell = async () => {
        console.log("Datos enviados:", formData);
        if (!validateForm()) return;

        try {
            await actions.sellProduct(formData, navigate, setShowSuccess);
            navigate("/");
        } catch (error) {
            console.error("Error al subir el producto:", error);
            alert("Hubo un error al subir el producto. Por favor, intenta de nuevo");
        }
    };
    useEffect(() => {
        window.scrollTo(0, 0);
        actions.setShowLoginModal(false);
    }, []);


    return (

        <div className="__sell_container__">
            {store.showLoginModal && <LoginModal />}
            {showSuccess && <PremiumModal />}
            <section className="text-center mb-4">
                <h1 className="title">¡Empieza a vender!</h1>
                <p className="subtitle">Fácil y rápido, con total seguridad. Garantía Final Boss.</p>
            </section>

            <section className="row align-items-center mb-4">
                <div className="col-md-4 d-flex justify-content-center">
                    <PhotoUpload onUploadSuccess={handleImageUpload} />
                </div>
                <div className="col-md-8 d-flex flex-column justify-content-center">
                    <p className="mb-3">
                        Sube tu foto, añade los datos y empieza a vender. Recuerda que puedes promocionar hasta dos
                        artículos sin coste extra con tu suscripción.
                    </p>
                    <div className="d-flex gap-2">
                        <button className="btn btn-success px-4 __premium_button__" onClick={handleGoToPremium}>Go to Premium</button>
                    </div>
                </div>
            </section>

            <section className="bg-dark text-light p-4 rounded">
                <form className="d-flex flex-column gap-4">
                    <div className="row">
                        <div className="col-md-6 d-flex flex-column __form_properties__">
                            <label htmlFor="name" className="mb-2">Nombre</label>
                            <input
                                type="text"
                                name="name"
                                id="name"
                                className="form-control"
                                value={formData.name}
                                placeholder="Nombre"
                                onChange={handleChange} required
                            />
                        </div>
                        <div className="col-md-6">
                            <div className="row g-2">
                                <div className="col-6 d-flex flex-column __form_properties__">
                                    <label htmlFor="category" className="mb-2">Categoría</label>
                                    <select
                                        name="category"
                                        id="category"
                                        className="form-select"
                                        onChange={(e) => updateTypeOptions(e.target.value)} required
                                    >
                                        <option value="">Selecciona</option>
                                        <option value="consolas">Consola</option>
                                        <option value="videojuegos">Videojuego</option>
                                        <option value="accesorios">Accesorios</option>
                                    </select>
                                </div>
                                <div className="col-6 d-flex flex-column __form_properties__">
                                    <label htmlFor="state" className="mb-2">Estado</label>
                                    <select
                                        name="state"
                                        id="state"
                                        className="form-select"
                                        value={formData.state}
                                        onChange={handleChange} required
                                    >
                                        <option value="">Selecciona</option>
                                        <option value="true">Nuevo</option>
                                        <option value="false">Usado</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-6 d-flex flex-column __form_properties__">
                            <label htmlFor="brand" className="mb-2">Marca</label>
                            <input
                                type="text"
                                name="brand"
                                id="brand"
                                className="form-control"
                                value={formData.brand}
                                placeholder="Marca"
                                onChange={handleChange} required
                            />
                        </div>
                        <div className="col-md-6 d-flex flex-column __form_properties__">
                            <label htmlFor="year" className="mb-2">Año</label>
                            <input
                                type="number"
                                name="year"
                                id="year"
                                className="form-control"
                                value={formData.year}
                                placeholder="Año"
                                min="1900"
                                onChange={handleChange} required
                            />
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-6 d-flex flex-column __form_properties__">
                            <label htmlFor="platform" className="mb-2">Plataforma</label>
                            <input
                                type="text"
                                name="platform"
                                id="platform"
                                className="form-control"
                                value={formData.platform}
                                placeholder="Plataforma"
                                onChange={handleChange} required
                            />
                        </div>
                        <div className="col-md-6 d-flex flex-column __form_properties__">
                            <label htmlFor="type" className="mb-2">Tipo</label>
                            <select
                                name="type"
                                id="type"
                                className="form-select"
                                value={formData.type}
                                onChange={handleChange}
                                required
                            >
                                <option value="">Selecciona</option>
                                {typeOptions.map((option, index) => (
                                    <option key={index} value={option}>
                                        {option}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>
                    <div className="d-flex flex-column __form_properties__">
                        <label htmlFor="description" className="mb-2">Descripción</label>
                        <textarea
                            name="description"
                            id="description"
                            className="form-control"
                            rows="3"
                            value={formData.description}
                            placeholder="Escribe una descripción..."
                            onChange={handleChange} required
                        ></textarea>
                    </div>
                    <div className="d-flex flex-column w-50">
                        <label htmlFor="price" className="mb-2">Precio</label>
                        <input
                            type="number"
                            name="price"
                            id="price"
                            value={formData.price}
                            className="__price_input__"
                            placeholder="€uros"
                            min="1.01"
                            onChange={handleChange} required
                        />
                    </div>
                    <div className="d-flex justify-content-center __sell_button__">
                        <button
                            type="button"
                            className="btn bt_sell px-5"
                            onClick={handleSell}>
                            Vender
                        </button>
                    </div>
                </form>
            </section>
        </div>
    );
};