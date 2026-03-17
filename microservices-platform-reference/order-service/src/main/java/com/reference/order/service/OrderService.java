package com.reference.order.service;

import com.reference.order.domain.Order;
import com.reference.order.events.OrderEvents;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.CopyOnWriteArrayList;

@Service
public class OrderService {

    private final List<Order> store = new CopyOnWriteArrayList<>();
    private final KafkaTemplate<String, String> kafkaTemplate;

    public OrderService(KafkaTemplate<String, String> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
        // Seed one order for demo
        store.add(new Order("1", "user-1", "prod-1", 2, "CREATED", Instant.now()));
    }

    public List<Order> findAll() {
        return List.copyOf(store);
    }

    public Optional<Order> findById(String id) {
        return store.stream().filter(o -> o.id().equals(id)).findFirst();
    }

    public Order create(String userId, String productId, int quantity) {
        Order order = new Order(
                UUID.randomUUID().toString(),
                userId,
                productId,
                quantity,
                "CREATED",
                Instant.now()
        );
        store.add(order);
        kafkaTemplate.send(OrderEvents.ORDER_CREATED, order.id(), "Order created: " + order.id());
        return order;
    }
}
