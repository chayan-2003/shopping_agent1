export type Product = {
  id: number;
  name: string;
  description: string;
  category: string;
  price: number;
  stock: number;
};

export type CartItem = {
  product_id: number;
  name: string;
  quantity: number;
  unit_price: number;
  line_total: number;
};

export type Cart = {
  session_id: string;
  items: CartItem[];
  total_items: number;
  subtotal: number;
};

export type OrderItem = {
  product_id: number;
  name: string;
  quantity: number;
  unit_price: number;
};

export type Order = {
  order_id: number;
  session_id: string;
  shipping_address: string;
  status: string;
  total_amount: number;
  created_at: string;
  items: OrderItem[];
};

export type ChatMessage = {
  role: 'user' | 'assistant';
  content: string;
};
