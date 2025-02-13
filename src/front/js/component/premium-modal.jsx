import React, { useContext } from "react";
import { Link } from "react-router-dom";
import "../../styles/modal.css";
import { Context } from "../store/appContext";

export const PremiumModal = () => {
    const { actions } = useContext(Context);

    const handleCloseModal = () => {
        actions.setShow(false); // Actualiza el estado global si lo necesitas
    };

    return (
        <div
            className="modal fade"
            id="premiumModal"
            tabIndex="-1"
            aria-labelledby="premiumModalLabel"
            aria-hidden="true"
        >
            <div className="modal-dialog modal-lg">
                <div className="modal-content">
                    <div className="modal-header">
                        <button
                            type="button"
                            className="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                            onClick={handleCloseModal}
                        ></button>
                    </div>
                    <div className="modal-body text-center">
                        <img
                            src="https://res.cloudinary.com/dshjlidcs/image/upload/v1738527220/web-img/o7qykckeyaqyrrzjbwxz.png"
                            alt="Premium-boss"
                            className="img-fluid"
                        />
                        <p>¡Tu producto se subió con éxito! 🎉</p>
                    </div>
                </div>
            </div>
        </div>
    );
};