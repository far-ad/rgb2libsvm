from itertools import count

def rgbd2libsvm(rgbd_data_file, rgbd_labels_file, libsvm_output_file):
    feature_start_index = 1

    rgbd_labels = open(rgbd_labels_file)
    # pop first line (contains the header)
    rgbd_labels.__next__()
    labels = set(rgbd_labels)
    rgbd_labels.close()

    libsvm_output = open(libsvm_output_file, 'w')

    header = True
    for (features, label) in zip(open(rgbd_data_file), open(rgbd_labels_file)):
        if header:
            (n_data_s, n_features_s) = features.split()
            (n_data, n_features) = (int(n_data_s), int(n_features_s))
            (n_labels_s, n_labels_features_s) = label.split()
            (n_labels, n_labels_features) = (int(n_labels_s), int(n_labels_features_s))
            assert(n_data == n_labels)

            libsvm_output.write('%d %d %d %d\n' % (n_data, n_features, len(labels), feature_start_index))
            header = False
            continue
        
        libsvm_output.write('%d' % (int(label)))

        for (feature_str, i) in zip(features.split(), count(feature_start_index)):
            feature = float(feature_str)
            if not abs(feature) < 0.00000001:
                libsvm_output.write(' %d:%f' % (i, feature))
        libsvm_output.write('\n')

    libsvm_output.close()

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 4:
        print('%s - usage:\n%s <rgbd-data-file> <rgbd-label-file> <libsvm-output-file>\n' % (sys.argv[0], sys.argv[0]))
        sys.exit(1)

    rgbd2libsvm(sys.argv[1], sys.argv[2], sys.argv[3])
