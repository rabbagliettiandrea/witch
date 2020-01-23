from invoke import Collection, Program

from witch import VERSION
from .tasks import dev, prod, utils, db, aws

namespace = Collection()
namespace.add_collection(prod)
namespace.add_collection(dev)
namespace.add_collection(db)
namespace.add_collection(utils)
namespace.add_collection(aws)
namespace.add_task(prod.deploy)

program = Program(namespace=namespace, version=VERSION)
