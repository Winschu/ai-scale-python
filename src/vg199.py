def network19(input_shape, num_classes):
    # Laden des VGG19 Modells
    vgg19_model = VGG19(weights='imagenet', include_top=False, input_shape=input_shape)

    # Setzen der Trainingparameter auf False
    for layer in vgg19_model.layers:
        layer.trainable = False

    img_input = Input(shape=input_shape, name='data')
    x = Lambda(convert_to_hsv_and_grayscale)(img_input)

    # Behalte nur die ersten drei Kanäle bei
    x = Lambda(lambda x: x[:, :, :, :3])(x)

    # Hinzufügen von VGG19 zu deinem Modell
    x = vgg19_model(x)

    x = Flatten()(x)
    x = Dense(1024, activation='relu', name='fcl1')(x)
    x = Dropout(0.2)(x)
    x = Dense(256, activation='relu', name='fcl2')(x)
    x = Dropout(0.2)(x)
    out = Dense(num_classes, activation='softmax', name='predictions')(x)
    model = Model(inputs=img_input, outputs=out)
    return model