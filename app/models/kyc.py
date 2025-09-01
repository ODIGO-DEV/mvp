from datetime import datetime
from app.extensions import db


class KYC(db.Model):
    __tablename__ = "kyc"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(50), default="pending")
    document_type = db.Column(db.String(50))
    front_document_url = db.Column(db.String(255))
    back_document_url = db.Column(db.String(255))

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<KYC {self.status}>"
