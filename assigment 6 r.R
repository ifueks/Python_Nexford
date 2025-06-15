install.packages("keras")
library(keras)
install_keras()

fashion <- dataset_fashion_mnist()
c(c(x_train, y_train), c(x_test, y_test)) %<-% fashion

# Reshape and normalize
x_train <- array_reshape(x_train, c(nrow(x_train), 28, 28, 1)) / 255
x_test <- array_reshape(x_test, c(nrow(x_test), 28, 28, 1)) / 255

# One-hot encoding
y_train <- to_categorical(y_train, 10)
y_test <- to_categorical(y_test, 10)

#Build CNN Model
model <- keras_model_sequential() %>%
  layer_conv_2d(filters = 32, kernel_size = c(3,3), activation = 'relu', input_shape = c(28, 28, 1)) %>%
  layer_max_pooling_2d(pool_size = c(2,2)) %>%
  layer_conv_2d(filters = 64, kernel_size = c(3,3), activation = 'relu') %>%
  layer_max_pooling_2d(pool_size = c(2,2)) %>%
  layer_flatten() %>%
  layer_dense(units = 128, activation = 'relu') %>%
  layer_dropout(0.5) %>%
  layer_dense(units = 10, activation = 'softmax')

model %>% compile(
  loss = 'categorical_crossentropy',
  optimizer = optimizer_adam(),
  metrics = 'accuracy'
  
  #to train model
  model %>% fit(
    x_train, y_train,
    epochs = 5, batch_size = 128,
    validation_split = 0.1
  )
  
  #To make predictions
  preds <- model %>% predict(x_test[1:2,,,])
  
  for (i in 1:2) {
    image(as.raster(x_test[i,,,1]), main = paste("Predicted:", which.max(preds[i,]) - 1))
  }
  
  